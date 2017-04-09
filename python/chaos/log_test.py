import logging

logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] (%(levelname)s) %(name)s: %(message)s')

logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# ch = logging.StreamHandler()
# ch.setLevel(logging.INFO)
# ch.setFormatter(formatter)


def main():
    logging.warn("asdf")
    logger.info("asdfasdfasdf")


if __name__ == '__main__':
    main()
