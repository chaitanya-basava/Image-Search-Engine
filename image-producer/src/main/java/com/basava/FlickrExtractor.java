package com.basava;

import com.flickr4java.flickr.REST;
import com.flickr4java.flickr.Flickr;
import com.flickr4java.flickr.people.User;
import com.flickr4java.flickr.photos.Photo;
import com.flickr4java.flickr.FlickrException;
import com.flickr4java.flickr.photos.PhotoList;
import com.flickr4java.flickr.people.PeopleInterface;
import com.flickr4java.flickr.photos.PhotosInterface;
import com.flickr4java.flickr.photos.SearchParameters;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Map;
import java.util.List;
import java.util.ArrayList;

public class FlickrExtractor {
    private final Flickr flickr;
    private final Logger logger = LoggerFactory.getLogger(FlickrExtractor.class);
    FlickrExtractor(Map<String, String> secrets) {
        this.flickr = new Flickr(secrets.get("API_KEY"), secrets.get("SECRET"), new REST());
    }

    List<FlickrImage> extract(int perPage, int page) {
        ArrayList<FlickrImage> flickrImages = new ArrayList<>();

        PhotosInterface photosInterface = flickr.getPhotosInterface();
        PeopleInterface peopleInterface = flickr.getPeopleInterface();

        try{
            SearchParameters params = new SearchParameters();
            params.setMedia("photos");

            PhotoList<Photo> photos = photosInterface.search(params, perPage, page);
            photos.forEach(photo ->
            {
                try {
                    if(photo.getMedium640Url() == null)
                        throw new FlickrException("Medium640 url can't be null");

                    User user = peopleInterface.getInfo(photo.getOwner().getId());
                    Photo photoDetails = photosInterface.getInfo(photo.getId(), null);

                    String[] userUrlId = user.getProfileurl().split("/");

                    FlickrImage image = FlickrImage.newBuilder()
                            .setTitle(photo.getTitle())
                            .setId(photo.getId())
                            .setImgUrl(photo.getMedium640Url())
                            .setUserUrlId(userUrlId[userUrlId.length - 1])
                            .setDescription(photoDetails.getDescription())
                            .setPostedOn(photoDetails.getDatePosted().getTime())
                            .build();

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
