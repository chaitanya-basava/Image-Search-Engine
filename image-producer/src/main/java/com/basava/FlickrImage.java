package com.basava;

public class FlickrImage {

    private final String title;
    private final String id;
    private final String imgUrl;
    private final String userName;
    private final String userRealName;
    private final String userUrl;

    FlickrImage(String title, String id, String imgUrl, String userName, String userRealName, String userUrl) {
        this.title = title;
        this.id = id;
        this.imgUrl = imgUrl;
        this.userName = userName;
        this.userRealName = userRealName;
        this.userUrl = userUrl;
    }

    @Override
    public String toString() {
        return "FlickrImage [id=" + id + ", title=" + title + ", imgUrl=" + imgUrl + ", userName=" + userName
                + ", userRealName=" + userRealName + ", userUrl=" + userUrl + "]";
    }
}
