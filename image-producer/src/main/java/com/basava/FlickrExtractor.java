package com.basava;

import com.flickr4java.flickr.REST;
import com.flickr4java.flickr.Flickr;
import com.flickr4java.flickr.people.User;
import com.flickr4java.flickr.FlickrException;
import com.flickr4java.flickr.people.PeopleInterface;
import com.flickr4java.flickr.photos.PhotosInterface;
import com.flickr4java.flickr.photos.SearchParameters;

import com.flickr4java.flickr.tags.Tag;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.*;
import java.util.*;
import java.nio.file.Paths;
import java.nio.file.Files;
import java.util.stream.Collectors;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;

public class FlickrExtractor {
    private final Random random = new Random();
    private final Flickr flickr;
    private final Map<String, Integer> tagCounts;
    private final Logger logger = LoggerFactory.getLogger(FlickrExtractor.class);
    private final String cachePath;
    private final Set<String> extras;

    FlickrExtractor(String cachePath) {
        Map<String, String> secrets = this.getSecrets();
        this.cachePath = cachePath;
        this.flickr = new Flickr(secrets.get("API_KEY"), secrets.get("SECRET"), new REST());
        this.tagCounts = this.loadTagsCache();

        this.extras = new LinkedHashSet<>();
        this.extras.add("date_upload");
        this.extras.add("tags");
    }

    List<FlickrImage> extract(int n) {
        String key = this.getRandomTagKey();
        int page = this.tagCounts.get(key);
        ArrayList<FlickrImage> flickrImages = new ArrayList<>();

        PhotosInterface photosInterface = flickr.getPhotosInterface();
        PeopleInterface peopleInterface = flickr.getPeopleInterface();

        try {
            SearchParameters params = new SearchParameters();
            params.setMedia("photos");
            params.setTags(key.split("_"));
            params.setTagMode("any");
            params.setExtras(this.extras);

            photosInterface.search(params, n, page).forEach(photo -> {
                try {
                    if (photo.getMedium640Url() == null)
                        throw new FlickrException("Medium640 url can't be null");

                    List<CharSequence> tags = photo.getTags()
                            .stream().map(Tag::getValue)
                            .collect(Collectors.toList());

                    User user = peopleInterface.getInfo(photo.getOwner().getId());
                    String[] userId = user.getProfileurl().split("/");
                    String[] imgUrl = photo.getMedium640Url().split("/");

                    FlickrImage image = FlickrImage.newBuilder()
                            .setTitle(photo.getTitle())
                            .setId(photo.getId())
                            .setImgUrl(imgUrl[3] + "/" + imgUrl[4])
                            .setUserId(userId[userId.length - 1])
                            .setUserName(user.getUsername())
                            .setPostedOn(photo.getDatePosted().getTime())
                            .setTags(tags)
                            .build();

                    flickrImages.add(image);
                } catch (FlickrException e) {
                    logger.error(e.getErrorMessage());
                }
            });

            this.updateTagValue(key);
        } catch (FlickrException e) {
            throw new RuntimeException(e);
        }

        return flickrImages;
    }

    // for testing FlickrExtractor class
    public static void main(String[] args) {
        FlickrExtractor extractor = new FlickrExtractor(args[0]);
        System.out.println(extractor.extract(1));
    }

    private String getRandomTagKey() {
        List<String> keyList = new ArrayList<>(this.tagCounts.keySet());
        int randIdx = random.nextInt(keyList.size());
        return keyList.get(randIdx);
    }

    private void updateTagValue(String key) {
        this.tagCounts.put(key, this.tagCounts.get(key) + 1);
    }

    Map<String, Integer> loadTagsCache() {
        try {
            InputStream inputStream = Files.newInputStream(Paths.get(cachePath));
            TypeReference<HashMap<String, Integer>> typeRef = new TypeReference<HashMap<String, Integer>>() {};
            ObjectMapper objectMapper = new ObjectMapper();

            return objectMapper.readValue(inputStream, typeRef);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    void updateTagsCache() {
        ObjectMapper mapper = new ObjectMapper();

        try {
            String jsonResult = mapper.writerWithDefaultPrettyPrinter().writeValueAsString(this.tagCounts);
            FileWriter file = new FileWriter(cachePath);
            file.write(jsonResult);
            file.close();

            logger.info("[UPDATED] tags at " + cachePath);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    private Map<String, String> getSecrets() {
        InputStream inputStream = FlickrExtractor.class.getClassLoader().getResourceAsStream("secrets.json");
        ObjectMapper objectMapper = new ObjectMapper();
        TypeReference<Map<String, String>> typeReference = new TypeReference<Map<String, String>>() {
        };

        try {
            return objectMapper.readValue(inputStream, typeReference);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
