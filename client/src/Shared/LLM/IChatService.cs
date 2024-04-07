using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Shared.LLM;

public interface IChatService
{
    Task<ChatMessageDto.Index?> GetIndexAsync(ChatMessageRequest.Index request, string uuid);
    Task<ChatMessageDto.Detail?> GetDetailAsync(ChatMessageRequest.Index request, string uuid);
    Task<string> StartChatAsync();
    Task<string> StopChatAsync(string uuid);
}
