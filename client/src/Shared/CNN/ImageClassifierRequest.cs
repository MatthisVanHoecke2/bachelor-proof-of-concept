using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Project.Shared.CNN;

public static class ImageClassifierRequest
{
    public class Index
    {
        public MultipartFormDataContent File { get; set; } = default!;
    }
}
