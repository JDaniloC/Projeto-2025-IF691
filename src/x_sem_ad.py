from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from evaluation.utils import generate_prediction_list
import pm4py, random, torch, re
import pandas as pd

DEFAULT_ACTIVITY_NAME = 'concept:name'
DEFAULT_CASE_ID_NAME = 'case:concept:name'

class XSemAD:
    def __init__(self, path_to_model: str, random_seed: int=4,
                    max_new_tokens: int=100, num_recommendations: int=30):
        self.num_recommendations = num_recommendations
        self.max_new_tokens = max_new_tokens
        self.path_to_model = path_to_model
        self.random_seed = random_seed
        print(f"Loading model from: {self.path_to_model} folder")
        try:
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.path_to_model)
            self.tokenizer = AutoTokenizer.from_pretrained(self.path_to_model)
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model = self.model.to(self.device)
        except:
            print('Error: Check model path!')

    def load_event_log(self, log: pd.DataFrame,
                       case_id_column_name: str=DEFAULT_CASE_ID_NAME,
                       activity_column_name: str=DEFAULT_ACTIVITY_NAME):
        """
        Load an event log from a file in XES format and prepare the context
        for constraint generation. In addition, it replaces multiple spaces
        with a single space and converts activity names to lowercase.

        Args:
            path_to_file: Path to the XES file.
            case_id_column_name: Name of the column containing case IDs.
            activity_column_name: Name of the column containing activity names.
        """
        self.activity_column_name = activity_column_name
        self.case_id_column_name = case_id_column_name
        self.log = log.copy()

        random.seed(self.random_seed)
        self.events = self.log[activity_column_name].unique()
        self.context = " <event> " + " <event> ".join(self.events)

    def _filter_items(self, prediction_list: list[tuple[str, float]],
                        events: list[str]) -> list[tuple[str, float]]:
        """
        Filter the prediction list to include only items that have a description
        containing at least one event from the provided list of events:
        1. Get the activities description (a, b) from the format "RULE[a, b]"
        2. Get the list of activities by splitting the description by commas
        3. Filter the prediction to remove duplicates activities
        4. Filter the prediction to include only those that contain
            at least one of the events from the activities list.

        Args:
            prediction_list: List of predictions, where each item
                is a tuple containing a description and a score.
            events: List of events to filter against.

        Returns:
            A filtered list of predictions that contain at least one event
            from the provided list in their description.
        """
        filtered_list = []
        for description, score in prediction_list:
            activities_description = re.search(r'\[(.*?)\]', description)
            if not activities_description:
                continue

            activities = activities_description.group(1).split(',')
            description_elements = [elem.strip() for elem in activities]
            
            # Check for duplicates in description elements
            if len(description_elements) != len(set(description_elements)):
                continue

            # Check if any of the description elements are in the second list
            if any(elem in events for elem in description_elements):
                filtered_list.append((description, score))
        return filtered_list

    def _filter_list_by_threshold(self, prediction_list: list[tuple[str, float]],
                                    threshold: float) -> list[tuple[str, float]]:
        """
        Filter the prediction list by a score threshold.

        Args:
            prediction_list: List of predictions, where each item
                is a tuple containing a description and a score.
            threshold: Score threshold for filtering.

        Returns:
            A filtered list of predictions that have a score greater than the threshold.
        """
        return [item for item in prediction_list if item[1] > threshold]

    def generate_constraint(self, constraint_type: str, threshold: float = .8):
        constraint_type = constraint_type.strip().capitalize()
        print('Get prediction for constraint type: ', constraint_type)
        prompt = f'{constraint_type}: {self.context}'
        prediction = generate_prediction_list(prompt, self.tokenizer, self.model,
                                                self.num_recommendations,
                                                self.max_new_tokens, self.device)
        prediction = self._filter_items(prediction, self.events)
        prediction = self._filter_list_by_threshold(prediction, threshold)
        return prediction

    ##################
    # CHECK FOR ANOMALIES
    ##################
    def check_init(self, trace, a):
        return trace[0] == a

    def check_end(self, trace, a):
        return trace[-1] == a

    def check_prec(self, trace, aj, ak):
        return ak not in trace or aj in trace[:trace.index(ak)]

    def check_alt_prec(self, trace, aj, ak):
        for i in range(1, len(trace)):
            if trace[i] == ak and trace[i-1] != aj:
                return False
        return True

    def check_co_ex(self, trace, aj, ak):
        return aj in trace and ak in trace

    def check_resp(self, trace, aj, ak):
        if aj in trace:
            return ak in trace[trace.index(aj):]
        return True

    def check_alt_resp(self, trace, aj, ak):
        last_aj_index = -1
        for i in range(len(trace)):
            if trace[i] == aj:
                if last_aj_index != -1 and ak not in trace[last_aj_index+1:i]:
                    return False
                last_aj_index = i
        return True

    def check_succ(self, trace, aj, ak):
        return aj not in trace or (ak in trace and trace.index(ak) == trace.index(aj) + 1)

    def check_alt_succ(self, trace, aj, ak):
        expected_next = None
        for a in trace:
            if a == aj:
                if expected_next and expected_next != ak:
                    return False
                expected_next = ak
            elif a == ak:
                if expected_next and expected_next != aj:
                    return False
                expected_next = aj
        return True

    def check_choice(self, trace, aj, ak):
        return aj in trace or ak in trace

    def check_ex_ch(self, trace, aj, ak):
        return (aj in trace) != (ak in trace)

    def apply_constraint(self, trace, constraint):
        """
        Apply a specific constraint to a trace and check if it holds.

        Args:
            trace: A list of activities representing the trace.
            constraint: A string representing the constraint to apply.

        Returns:
            True if the constraint holds, False otherwise.
        """
        if constraint.startswith('Init'):
            a = constraint[len('Init['):-1]
            return self.check_init(trace, a)
        elif constraint.startswith('End'):
            a = constraint[len('End['):-1]
            return self.check_end(trace, a)
        elif constraint.startswith('Precedence'):
            aj, ak = constraint[len('Precedence['):-1].split(', ')
            return self.check_prec(trace, aj, ak)
        elif constraint.startswith('Alternate Precedence'):
            aj, ak = constraint[len('Alternate Precedence['):-1].split(', ')
            return self.check_alt_prec(trace, aj, ak)
        elif constraint.startswith('Co-Existence'):
            aj, ak = constraint[len('Co-Existence['):-1].split(', ')
            return self.check_co_ex(trace, aj, ak)
        elif constraint.startswith('Response'):
            aj, ak = constraint[len('Response['):-1].split(', ')
            return self.check_resp(trace, aj, ak)
        elif constraint.startswith('Alternate Response'):
            aj, ak = constraint[len('Alternate Response['):-1].split(', ')
            return self.check_alt_resp(trace, aj, ak)
        elif constraint.startswith('Succession'):
            aj, ak = constraint[len('Succession['):-1].split(', ')
            return self.check_succ(trace, aj, ak)
        elif constraint.startswith('Alternate Succession'):
            aj, ak = constraint[len('Alternate Succession['):-1].split(', ')
            return self.check_alt_succ(trace, aj, ak)
        elif constraint.startswith('Choice'):
            aj, ak = constraint[len('Choice['):-1].split(', ')
            return self.check_choice(trace, aj, ak)
        elif constraint.startswith('Exclusive Choice'):
            aj, ak = constraint[len('Exclusive Choice['):-1].split(', ')
            return self.check_ex_ch(trace, aj, ak)
        return False

    def count_violations(self, prediction):
        """
        Count the number of violations for each constraint in the prediction
        list across all traces in the event log.

        Args:
            prediction: A list of tuples where each tuple contains a constraint
                and its score, e.g., [('Init[a]', 0.9), ('End[b]', 0.8), ...].

        Returns:
            A dictionary where keys are constraints and values are the
            number of violations.
        """
        violations = {constraint: 0 for constraint, _ in prediction}
        for _, group in self.log.groupby(self.case_id_column_name):
            trace = group[self.activity_column_name].tolist()
            for constraint, _ in prediction:
                if not self.apply_constraint(trace, constraint):
                    violations[constraint] += 1
        return violations

    def run(self, constraint_type: str, threshold: float = 0.8):
        """
        Run the anomaly detection process for a specific constraint type.

        Args:
            constraint_type: The type of constraint to check.
            threshold: The score threshold for filtering predictions.

        Returns:
            A dictionary with constraints and their violation counts.
        """
        prediction = self.generate_constraint(constraint_type, threshold)
        return self.count_violations(prediction)

    def run_all(self, threshold: float = 0.8):
        """
        Run the anomaly detection process for all constraint types.

        Args:
            threshold: The score threshold for filtering predictions.

        Returns:
            A dictionary with constraint types as keys and their violation counts
            as values.
        """
        results = {}
        for constraint_type in ['Init', 'End', 'Precedence', 'Succession',
                                'Alternate Precedence', 'Co-Existence',
                                'Response', 'Alternate Response',
                                'Alternate Succession', 'Choice',
                                'Exclusive Choice']:
            results[constraint_type] = self.run(constraint_type, threshold)
        return results

def load_event_log_from_xes(path_to_file: str,
                            activity_column_name: str=DEFAULT_ACTIVITY_NAME):
    """
    Load an event log from a file in XES format and prepare the context
    for constraint generation. In addition, it replaces multiple spaces
    with a single space and converts activity names to lowercase.

    Args:
        path_to_file: Path to the XES file.
        activity_column_name: Name of the column containing activity names.
    """
    log = pm4py.read_xes(path_to_file)
    log = pm4py.convert_to_dataframe(log)
    log[activity_column_name] = log[activity_column_name].str.replace('  ',' ').str.lower()
    return log
