from confluent_kafka import Producer

from src.configs import settings


class KafkaProducer:
    _producer = None
    topic = settings.kafka_topic

    @property
    def producer(self):
        if self._producer is None:
            self._producer = Producer(
                {
                    "bootstrap.servers": settings.kafka_endpoint,
                    "sasl.mechanism": "PLAIN",
                    "security.protocol": "SASL_SSL",
                }
            )
        return self._producer

    def produce(self, data):
        self.producer.produce(self.topic, data)

    def close(self):
        self.producer.flush(1)


kafka_producer = KafkaProducer()


def kafka_logging(data):
    kafka_producer.produce(data)
