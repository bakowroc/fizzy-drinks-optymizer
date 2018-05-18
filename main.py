from Bar.Bar import Bar
from RabbitMQ.RabbitMQ import RabbitMQ
from config.Config import Config


def main():
    rabbit = RabbitMQ()
    body = "Beer"
    rabbit.publish(body, Config.RABBIT.QUEUES['ToBar'])

    bar = Bar()
    bar.start()


if __name__ == "__main__":
    main()
