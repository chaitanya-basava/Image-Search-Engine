package com.basava;

import com.flickr4java.flickr.Flickr;
import com.flickr4java.flickr.FlickrException;
import com.flickr4java.flickr.REST;
import com.flickr4java.flickr.people.PeopleInterface;
import com.flickr4java.flickr.people.User;
import com.flickr4java.flickr.photos.Photo;
import com.flickr4java.flickr.photos.PhotoList;
import com.flickr4java.flickr.photos.PhotosInterface;
import com.flickr4java.flickr.photos.SearchParameters;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class FlickrExtractor {
    private final Flickr flickr;
    private final Logger logger = LoggerFactory.getLogger(FlickrExtractor.class);
    FlickrExtractor(Map<String, String> secrets) {
        this.flickr = new Flickr(secrets.get("API_KEY"), secrets.get("SECRET"), new REST());
    }

    List<FlickrImage> extract() {
        ArrayList<FlickrImage> flickrImages = new ArrayList<>();

        PhotosInterface photosInterface = flickr.getPhotosInterface();
        PeopleInterface peopleInterface = flickr.getPeopleInterface();

        try{
            SearchParameters params = new SearchParameters();
            params.setMedia("photos");

            PhotoList<Photo> photos = photosInterface.search(params, 10, 1);
            photos.forEach(photo ->
            {
                try {
                    User user = peopleInterface.getInfo(photo.getOwner().getId());

                    FlickrImage image = new FlickrImage(
                            photo.getTitle(),
                            photo.getId(),
                            photo.getMedium640Url(),
                            user.getUsername(),
                            user.getRealName(),
                            user.getProfileurl()
                    );
                    flickrImages.add(image);
                } catch (FlickrException e) {
                    logger.error(e.getErrorMessage());
                }
            });
        } catch (FlickrException e) {
            throw new RuntimeException(e);
        }

        return flickrImages;
    }
}
