package com.basava;

import io.confluent.kafka.serializers.KafkaAvroSerializer;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.common.serialization.StringSerializer;

import java.util.Properties;

public class KafkaProducerManager<T> implements AutoCloseable {
    final Producer<String, T> producer;

    KafkaProducerManager() {
        String kafkaServerAddress = System.getenv()
                .getOrDefault("KAFKA_SERVER_ADDRESS", "localhost:9092");
        String schemaRegistryServerUrl = System.getenv()
                .getOrDefault("SCHEMA_REGISTRY_SERVER_URL", "http://localhost:8081");

        Properties kafkaProps = new Properties();
        kafkaProps.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, kafkaServerAddress);
        kafkaProps.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        kafkaProps.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, KafkaAvroSerializer.class.getName());
        kafkaProps.put("schema.registry.url", schemaRegistryServerUrl);

        this.producer = new KafkaProducer<>(kafkaProps);
    }

    @Override
    public void close() {
        this.producer.close();
    }
}
