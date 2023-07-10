class Handlers:

    @staticmethod
    def handle_creative_tone(ack, body, logger):
        ack()
        logger.info(body)
        # print("Creative tone action triggered")
        return 0.9

    @staticmethod
    def handle_balanced_tone(ack, body, logger):
        ack()
        logger.info(body)
        # print("Balanced tone action triggered")
        return 0.7

    @staticmethod
    def handle_precise_tone(ack, body, logger):
        ack()
        logger.info(body)
        # print("Precise tone action triggered")
        return 0.4
