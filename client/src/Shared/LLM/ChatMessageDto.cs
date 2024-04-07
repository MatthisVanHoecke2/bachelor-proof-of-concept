using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Shared.LLM;

public static class ChatMessageDto
{
    public class Mutate
    {
        public MessageSender Sender { get; set; }
        public string Message { get; set; } = default!;
    }

    public class Index
    {
        public string Input { get; set; } = default!;
        public string Output { get; set; } = default!;
    }

    public class Detail
    {
        public MessageSender Sender { get; set; }
        public ChatHistoryDto ChatHistoryDto { get; set; } = default!;
        public string Message { get; set; } = default!;
    }
}
