using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Project.Shared.LLM;

namespace Project.Shared.CNN;

public interface IImageClassifierService
{
    Task<ImageClassifierDto.Index?> PostImageAsync(MultipartFormDataContent request);
}
