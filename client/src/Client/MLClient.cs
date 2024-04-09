namespace Project.Client;

public class MLClient
{
    public HttpClient Client { get; }

    public MLClient(HttpClient client)
    {
        this.Client = client;
    }
}
