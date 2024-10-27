// script.js
const chatInput = 
	document.querySelector('.chat-input textarea');
const sendChatBtn = 
	document.querySelector('.chat-input button');
const chatbox = document.querySelector(".chatbox");

let userMessage;

const createChatLi = (message, className) => {
	const chatLi = document.createElement("li");
	chatLi.classList.add("chat", className);
	let chatContent = 
		className === "chat-outgoing" ? `<p>${message}</p>` : `<p>${message}</p>`;
	chatLi.innerHTML = chatContent;
	return chatLi;
}

async function generateResponse(incomingChatLi) {
	
}

	// Example usage:

const handleChat = () => {
	userMessage = chatInput.value.trim();
	if (!userMessage) {
		return;
	}
	chatbox
	.appendChild(createChatLi(userMessage, "chat-outgoing"));
	chatbox
	.scrollTo(0, chatbox.scrollHeight);

	setTimeout(() => {
		const incomingChatLi = createChatLi("Suy nghĩ...", "chat-incoming")
		chatbox.appendChild(incomingChatLi);
		chatbox.scrollTo(0, chatbox.scrollHeight);
		generateResponse(incomingChatLi);
	}, 600);
}

sendChatBtn.addEventListener("click", handleChat);
var chatbotcomplete = document.querySelector(".chatBot");
var toggleChatBot=document.querySelector('.toggleChatBot')


function cancel() {
	chatbotcomplete.style.scale = "0";
	setTimeout(function(){
		toggleChatBot.style.display="block"
	},210)
	
}
function openChatBot(){
	chatbotcomplete.style.scale = "1";
	toggleChatBot.style.display="none"

}
