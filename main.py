import logging

from controller import CSVController


def main():
    logging.basicConfig(level=logging.ERROR)
    controller = CSVController()
    controller.run()

if __name__ == '__main__':
    main()
