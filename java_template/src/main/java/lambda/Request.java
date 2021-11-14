package lambda;

/**
 *
 * @author Wes Lloyd
 */
public class Request {

    String name;
    private String bucketname;
    private String filename;
    

    public String getBucketname() {
        return bucketname;
    }
    
    public String getFilename() {
        return filename;
    }
    
    public void setBucketname() {
        this.bucketname = bucketname;
    }
    
    public void setFilename() {
        this.filename = filename;
    }
    
    public String getName() {
        return name;
    }
    
    public String getNameALLCAPS() {
        return name.toUpperCase();
    }

    public void setName(String name) {
        this.name = name;
    }

    public Request(String name) {
        this.name = name;
    }

    public Request() {

    }
}
