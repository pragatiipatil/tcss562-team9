package lambda;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import saaf.Inspector;
import saaf.Response;
import java.util.HashMap;

/**
 * uwt.lambda_test::handleRequest
 *
 * @author Wes Lloyd
 * @author Robert Cordingly
 */
public class HelloPOJO implements RequestHandler<Request, HashMap<String, Object>> {

    /**
     * Lambda Function Handler
     * 
     * @param request Request POJO with defined variables from Request.java
     * @param context 
     * @return HashMap that Lambda will automatically convert into JSON.
     */
    public HashMap<String, Object> handleRequest(Request request, Context context) {
        
        //Collect inital data.
        Inspector inspector = new Inspector();
        inspector.inspectAll();
        
        //****************START FUNCTION IMPLEMENTATION*************************
        //Add custom key/value attribute to SAAF's output. (OPTIONAL)
        inspector.addAttribute("message", "Hello " + request.getName() 
                + "! This is an attributed added to the Inspector!");
        String bucketname = request.getBucketname();
        String filename = request.getFilename();
        
        AmazonS3 s3Client = AmazonS3ClientBuilder.standard().build();         
    //get object file using source bucket and srcKey name
    S3Object s3Object = s3Client.getObject(new GetObjectRequest(srcBucket, srcKey));
    //get content of the file
    InputStream objectData = s3Object.getObjectContent();
    //scanning data line by line
    String text = "";
    Scanner scanner = new Scanner(objectData);
    while (scanner.hasNext()) {
    text += scanner.nextLine();
    }
scanner.close();
        
        
        //Create and populate a separate response object for function output. (OPTIONAL)
        Response response = new Response();
        response.setValue("Hello " + request.getNameALLCAPS()
                + "! This is from a response object!");
        
        inspector.consumeResponse(response);
        
        //****************END FUNCTION IMPLEMENTATION***************************
        
        //Collect final information such as total runtime and cpu deltas.
        inspector.inspectAllDeltas();
        return inspector.finish();
    }
}
