package com.basava;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.io.InputStream;
import java.util.List;
import java.util.Map;

public class Main {
    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static final String KAFKA_TOPIC_NAME = System.getenv()
            .getOrDefault("KAFKA_TOPIC_NAME", "flickr-images");

    private static Map<String, String> getSecrets() {
        InputStream inputStream = Main.class.getClassLoader().getResourceAsStream("secrets.json");
        ObjectMapper objectMapper = new ObjectMapper();
        TypeReference<Map<String, String>> typeReference = new TypeReference<Map<String, String>>() {};

        try {
            return objectMapper.readValue(inputStream, typeReference);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public static void main(String[] args) {
        Map<String, String> secrets = Main.getSecrets();
        FlickrExtractor extractor = new FlickrExtractor(secrets);

        try(
                KafkaProducerManager<FlickrImage> producerManager =
                        new KafkaProducerManager<>(System.getenv("KAFKA_RUN_TYPE"))
        ) {
            List<FlickrImage> images = extractor.extract();
            // images.forEach(image -> logger.info(image.toString()));

            images.forEach(image -> {
                ProducerRecord<String, FlickrImage> imageRecord = new ProducerRecord<>(
                        Main.KAFKA_TOPIC_NAME, image.getId().toString(), image
                );

                producerManager.producer.send(imageRecord, (recordMetadata, e) -> {
                    if (e == null) {
                        logger.info("Success " + recordMetadata.toString());
                    } else {
                        logger.error(e.getMessage());
                    }
                });
            });

            producerManager.producer.flush();
        } catch (Exception e) {
            throw new RuntimeException(e);
        } finally {
            extractor.updateTagsCache();
        }
    }
}
