package com.bigData;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.JsonNodeFactory;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.KeyValue;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.kstream.*;

import java.io.IOException;
import java.util.LinkedList;


/**
 * Created by DELL on 16-Jan-19.
 */
public class logProcessor {


    public static void main(String[] args) {


        configuration config = new configuration();

        //System.out.println(config.getConfig().getProperty(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG));
        StreamsBuilder builder = new StreamsBuilder();


        Utils utils = new Utils();

        KStream<String,JsonNode> input = builder.stream(config.getInputTopicName(), Consumed.with(Serdes.String(), utils.jsonSerde));


        KTable<String,streamList> table = input.map((k, v) ->
                {
                    streamList newClass = new streamList();
                    String event_id = v.get("event_id").asText();
                    int val = utils.map(event_id);
                    int offset = v.get("offset").asInt();
                    newClass.l1 = new LinkedList<Integer>();
                    newClass.l1.add(val);
                    newClass.offset = offset;


                    return new KeyValue<String, streamList>(k, newClass);
                }
        )
         .groupByKey(Serialized.with(Serdes.String(), utils.getstreamListSerde()))
                .reduce((x, y) ->

                        {
                            x.l1.addAll(y.l1);


                            x.offset = y.offset;
                            int sizeCounter = x.l1.size();

                            return x;


                        }

                );



        KStream<String,JsonNode> prediction = table.toStream()
                .map( (k,v) ->

                        {


                            ObjectNode node = JsonNodeFactory.instance.objectNode();

                            node = utils.createArray(node);


                            try {
                                node = utils.addToArray(node,v.l1);
                            } catch (IOException e) {
                                e.printStackTrace();
                            }


                            ObjectNode predictionJson = JsonNodeFactory.instance.objectNode();

                            String pred = "12";

                            int[] buffer = utils.toIntArray(v.l1);
                            predictionJson = Predict.prediction(buffer,k);
                            //pred = Predict.prediction();
                            node.put("key",k);

                            node.put("offset",v.offset);
                            node.put("prediction",predictionJson.get("predictions"));
                           return new KeyValue<String, JsonNode>(k, node);
                        }


                );




        prediction.to(config.getOutputTopicName(), Produced.with(Serdes.String(), utils.getJsonSerde()));

        prediction.peek((k, v) -> {
                    System.out.println("key :" + k + " value: " + v);
                }
        );
        KafkaStreams streams = new KafkaStreams(builder.build(), config.getConfig());

        streams.start();


    }


}
