package com.basava;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;

import java.io.IOException;
import java.io.InputStream;
import java.util.List;
import java.util.Map;

public class Main {
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
        List<FlickrImage> flickrImages = extractor.extract();

        flickrImages.forEach(System.out::println);
    }
}
