using Microsoft.AspNetCore.Components;
using Microsoft.AspNetCore.Components.Forms;
using Microsoft.Extensions.Logging;
using MudBlazor;
using System.Net.Http;
using Project.Shared.CNN;
using System.Net.Http.Headers;
using Tewr.Blazor.FileReader;

namespace Project.Client.CNN;

public partial class Index
{
    bool success;
    string[] errors = { };
    public MudForm form { get; set; } = default!;
    private ImageClassifierDto.Mutate model = new();
    private ImageClassifierDto.Mutate.Validator ValidationRules = new();
    private string base64String = default!;
    private ImageClassifierDto.Index? response;
    private string? httpError;
    [Inject] ILogger<Index> Logger { get; set; } = default!;
    [Inject] public IFileReaderService FileReaderService { get; set; } = default!;

    [Inject] public IImageClassifierService ImageClassifierService { get; set; } = default!;

    private async Task Submit()
    {
        await form.Validate();

        if (form.IsValid)
        {
            try
            {
                MultipartFormDataContent formContent = ConvertImageToMultiPartFile(model.File!);
                response = await ImageClassifierService.PostImageAsync(formContent);
            }
            catch (Exception ex)
            {
                Logger.LogError(ex, ex.Message);
                httpError = "Failed to connect to server, please make sure the back-end is running.";
            }
        }
    }

    private MultipartFormDataContent ConvertImageToMultiPartFile(IBrowserFile file)
    {
        var formData = new MultipartFormDataContent();
        var fileStream = file.OpenReadStream(1024*1024*10);
        formData.Add(new StreamContent(fileStream), "file", file.Name);
        return formData;
    }

    private void UploadFiles(IBrowserFile file)
    {
        this.model.File = file;
        response = null;
        httpError = null;
        if (ValidationRules.Validate(model).IsValid) HandleFile(file);
    }

    private async void HandleFile(IBrowserFile file)
    {
        if (file != null)
        {
            var buffer = new byte[file.Size];
            using (var stream = file.OpenReadStream(8000000))
            {
                await stream.ReadAsync(buffer, 0, buffer.Length);
            }
            base64String = $"data:image/png;base64,{Convert.ToBase64String(buffer)}";
            StateHasChanged();
        }
    }
}
