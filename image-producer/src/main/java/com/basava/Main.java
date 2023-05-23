package com.basava;

import org.apache.commons.cli.*;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;

public class Main {
    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static final String KAFKA_TOPIC_NAME = System.getenv()
            .getOrDefault("KAFKA_TOPIC_NAME", "flickr-images");

    private static CommandLine parseArgs(String[] args) {
        Options options = new Options();

        Option kafkaProperties = new Option("kp", "kafkaProperties", true, "Kafka properties file path");
        kafkaProperties.setRequired(true);
        options.addOption(kafkaProperties);

        Option cacheFile = new Option("c", "cacheFile", true, "Kafka properties file path");
        kafkaProperties.setRequired(true);
        options.addOption(cacheFile);

        Option k = new Option("k", "iterations", true, "Number of iterations");
        options.addOption(k);

        CommandLineParser parser = new DefaultParser();
        HelpFormatter formatter = new HelpFormatter();

        try {
            return parser.parse(options, args);
        } catch (ParseException e) {
            System.out.println(e.getMessage());
            formatter.printHelp("utility-name", options);

            System.exit(1);
        }

        return null;
    }

    public static void main(String[] args) {
        CommandLine cmd = Main.parseArgs(args);
        String kafkaPropertiesFilePath = cmd.getOptionValue("kafkaProperties");
        String cachePath = cmd.getOptionValue("cacheFile");
        int k = cmd.hasOption("k") ? Integer.parseInt(cmd.getOptionValue("k")) : 10;

        if (k <= 0) {
            throw new IllegalArgumentException("k must be positive");
        }
        logger.info(String.format("Will be iterating for %d iterations.", k));
        logger.info(kafkaPropertiesFilePath);
        logger.info(cachePath);

        FlickrExtractor extractor = new FlickrExtractor(cachePath);

        try (
                KafkaProducerManager<FlickrImage> producerManager =
                        new KafkaProducerManager<>(kafkaPropertiesFilePath)
        ) {
            int iteration = 1;
            final int[] msgsUploaded = {0};

            while (iteration <= k) {
                List<FlickrImage> images = extractor.extract(10);

                images.forEach(image -> {
                    ProducerRecord<String, FlickrImage> imageRecord =
                            new ProducerRecord<>(Main.KAFKA_TOPIC_NAME, image.getId().toString(), image);

                    producerManager.producer.send(imageRecord, (recordMetadata, e) -> {
                        if (e != null) {
                            logger.error(e.getMessage());
                        } else {
                            msgsUploaded[0]++;
                        }
                    });
                });
                producerManager.producer.flush();

                logger.info(String.format("uploaded %d records in iteration %d", msgsUploaded[0], iteration));
                iteration++;
            }
        } catch (Exception e) {
            throw new RuntimeException(e);
        } finally {
            extractor.updateTagsCache();
        }
    }
}
