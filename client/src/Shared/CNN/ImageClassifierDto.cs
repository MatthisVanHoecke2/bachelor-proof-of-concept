using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Project.Shared.CNN;

public static class ImageClassifierDto
{
    public class Index
    {
        public string Prediction { get; set; } = default!;
        public double Confidence { get; set; }
    }
    public class Mutate
    {
        public IBrowserFile? File { get; set; }

        public class Validator : AbstractValidator<Mutate>
        {
            public Validator()
            {
                RuleFor(x => x.File)
                .NotEmpty();
                When(x => x.File != null, () =>
                {
                    RuleFor(x => x.File!.Size).LessThanOrEqualTo(10485760).WithMessage("The maximum file size is 10 MB");
                    RuleFor(x => x.File!.Name).Must(str => str.EndsWith(".png") || str.EndsWith(".jpg") || str.EndsWith(".jpeg")).WithMessage("File must be an image (png, jpg).");
                });
            }

            public Func<object, string, Task<IEnumerable<string>>> ValidateValue => async (model, propertyName) =>
            {
                var result = await ValidateAsync(ValidationContext<Mutate>.CreateWithOptions((Mutate)model, x => x.IncludeProperties(propertyName)));
                if (result.IsValid)
                    return Array.Empty<string>();
                return result.Errors.Select(e => e.ErrorMessage);
            };
        }
    }
}
