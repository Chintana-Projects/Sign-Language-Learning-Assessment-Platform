from app.ai.engine.ai_engine import AIEngine

from app.ai.sequence.temporal_buffer import TemporalBuffer
from app.ai.sequence.sequence_generator import SequenceGenerator
from app.ai.sequence.sequence_model import SequenceModel
from app.ai.sequence.sentence_builder import SentenceBuilder


class LiveRecognitionPipeline:
    """
    Future Live Recognition Pipeline

    Current:
        Webcam
            ↓
        AIEngine
            ↓
        Static Gesture Prediction

    Future:
        Webcam
            ↓
        AIEngine
            ↓
        Temporal Buffer
            ↓
        Sequence Generator
            ↓
        Sequence Model
            ↓
        Sentence Builder
    """

    def __init__(self):

        self.ai_engine = AIEngine()

        self.temporal_buffer = TemporalBuffer()

        self.sequence_generator = SequenceGenerator()

        self.sequence_model = SequenceModel()

        self.sentence_builder = SentenceBuilder()

    # --------------------------------------------------
    # Current Static Prediction
    # --------------------------------------------------

    def predict_static(self, image):

        return self.ai_engine.predict_image(image)

    # --------------------------------------------------
    # Future Continuous Prediction
    # --------------------------------------------------

    def predict_sequence(self, feature_vector):

        self.temporal_buffer.add_frame(feature_vector)

        if not self.temporal_buffer.is_ready():

            return None

        sequence = self.sequence_generator.generate_batch(
            self.temporal_buffer.get_sequence()
        )

        prediction = self.sequence_model.predict(sequence)

        return prediction