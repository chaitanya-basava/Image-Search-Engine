package com.basava;

import org.apache.kafka.clients.producer.ProducerRecord;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;

public class Main {
    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static final String KAFKA_TOPIC_NAME = System.getenv()
            .getOrDefault("KAFKA_TOPIC_NAME", "flickr-images");

    public static void main(String[] args) {
        if (args.length < 2) {
            throw new RuntimeException("pass kafka properties and tags cache json files path");
        }

        String kafkaPropertiesFilePath = args[0];
        String cachePath = args[1];

        int k;
        if (args.length == 3) {
            k = Integer.parseInt(args[2]);
        } else {
            k = 10;
        }
        logger.info(String.format("Will be iterating for %d iterations.", k));

        FlickrExtractor extractor = new FlickrExtractor(cachePath);

        try (
                KafkaProducerManager<FlickrImage> producerManager =
                        new KafkaProducerManager<>(kafkaPropertiesFilePath)
        ) {
            int iteration = 0;
            final int[] msgsUploaded = {0};

            while (iteration < k) {
                List<FlickrImage> images = extractor.extract(10);

                images.forEach(image -> {
                    ProducerRecord<String, FlickrImage> imageRecord = new ProducerRecord<>(
                            Main.KAFKA_TOPIC_NAME, image.getId().toString(), image
                    );

                    producerManager.producer.send(imageRecord, (recordMetadata, e) -> {
                        if (e != null) {
                            logger.error(e.getMessage());
                        } else {
                            msgsUploaded[0]++;
                        }
                    });
                });

                logger.info(String.format("uploaded %d records in iteration %d", msgsUploaded[0], iteration));
                iteration++;
            }

            producerManager.producer.flush();
        } catch (Exception e) {
            throw new RuntimeException(e);
        } finally {
            extractor.updateTagsCache();
        }
    }
}
