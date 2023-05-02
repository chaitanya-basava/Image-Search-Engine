package com.basava;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;
import com.flickr4java.flickr.Flickr;
import com.flickr4java.flickr.FlickrException;
import com.flickr4java.flickr.REST;
import com.flickr4java.flickr.photos.Photo;
import com.flickr4java.flickr.photos.PhotoList;
import com.flickr4java.flickr.photos.PhotosInterface;
import com.flickr4java.flickr.photos.SearchParameters;

import java.io.IOException;
import java.io.InputStream;
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

    public static void main(String[] args) throws FlickrException {
        Map<String, String> secrets = Main.getSecrets();

        Flickr flickr = new Flickr(secrets.get("API_KEY"), secrets.get("SECRET"), new REST());
        PhotosInterface photosInterface = flickr.getPhotosInterface();

        SearchParameters params = new SearchParameters();
        params.setMedia("photos");

        PhotoList<Photo> results = photosInterface.search(params, 10, 1);
        results.forEach(p ->
        {
            System.out.printf("Title: %s%n", p.getTitle());
            System.out.printf("ID: %s%n", p.getId());
            System.out.printf("Original Photo URL: %s%n", p.getMedium640Url());
        });
    }
}
