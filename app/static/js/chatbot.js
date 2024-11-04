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
	const apiKey = "AIzaSyAGAUKIZEwVqGqSXSsaZ3AMa6PJ9SlCXvI"; // Replace with your actual API key
	const messageElement = incomingChatLi.querySelector("p")
	try {
		const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`, {
		method: 'POST',
		headers: {
			"Content-Type": "application/json"
		},
		body: JSON.stringify({
			contents:[{
				role:"user",
				parts:[{ text:userMessage }]
			}],
		})
		});

		const data = await response.json();
		const message=data?.candidates[0].content.parts[0].text
		messageElement
			.textContent = message;
	} catch (error) {
		messageElement
			.classList.add("error");
			messageElement
			.textContent = "Có lỗi xảy ra.";
	} finally {
		chatbox.scrollTo(0, chatbox.scrollHeight)
	}
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
