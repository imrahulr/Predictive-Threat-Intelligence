package com.bigData;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.JsonNodeFactory;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.ContentType;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.util.EntityUtils;

import java.io.IOException;

/**
 * Created by DELL on 17-Jan-19.
 */
public class Predict {

    private static String ipAddress = "192.168.0.118";
    private static int port = 5000;
    private static String path = "/predict";

    public static ObjectNode prediction(int arr[],String sessionid)
    {


        ObjectNode node = JsonNodeFactory.instance.objectNode();


        //String prediction = "[1,7,8,75]";


        ObjectMapper mapper = new ObjectMapper();
        ArrayNode array = mapper.valueToTree(arr);
        HttpClient httpClient = HttpClientBuilder.create().build();

        node.putArray("seq").addAll(array);


        node.put("sessionid",sessionid);

        StringEntity entity = new StringEntity(node.toString(),
                ContentType.APPLICATION_JSON);

        HttpPost request = new HttpPost("http://"+ipAddress+":"+port+path);
        request.setEntity(entity);


        try {
            HttpResponse response = httpClient.execute(request);

            HttpEntity responseEntity = response.getEntity();

            if(responseEntity!=null) {
                node.put("predictions", EntityUtils.toString(responseEntity));

            }
        } catch (IOException e) {
            e.printStackTrace();
        }



        //node.put("predictions",prediction);



        return node;

    }



}
