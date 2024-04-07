using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Shared.LLM;

public class ChatHistoryDto
{
    public List<ChatMessageDto.Mutate> MessageHistory { get; set; } = new();
}
