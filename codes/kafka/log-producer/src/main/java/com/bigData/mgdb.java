package com.bigData;
import com.mongodb.MongoClientSettings;
import com.mongodb.ServerAddress;
import com.mongodb.client.*;
import org.bson.Document;
import java.util.Arrays;

/**
 * Created by DELL on 20-May-19.
 */

public class mgdb {

    public MongoClient mongoClient;
    public String ip = "192.168.0.101";
    public int port = 27017;
    mgdb()
    {
        mongoClient =  MongoClients.create(
                MongoClientSettings.builder()
                        .applyToClusterSettings(builder ->
                                builder.hosts(Arrays.asList(new ServerAddress(ip, port))))
                        .build());
    }





    public MongoCollection<Document> getData (String collName) {
        MongoDatabase database = mongoClient.getDatabase("CowrieHP");

        MongoCollection<Document> collection = database.getCollection(collName);


        return collection;
    }



}
