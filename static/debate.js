const chatData = [
    { role: "assistant", content: "You are friendly chatbot." },
    { role: "user", content: "Hi, my name is Isa" },
    {
      role: "assistant",
      content: "Hi Isa! It's nice to meet you. Is there anything I can help you with today?",
    },
    { role: "user", content: "Yes, you can remind me, What is my name?" },
  ];
  
  const conversation = document.getElementById("conversation");
  const messageInput = document.getElementById("message-input");
  const sendButton = document.getElementById("send-button");
  sendButton.onclick = async ()=>{
    const input = messageInput.value;
    const data = {"topic": input}
    for (let i = 0; i <= 4; i++) {
      console.log(data);
      const response = await fetch("/debate", {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
      });
      const content = await response.json();
      const role = (i % 2 === 0 ? "assistant" : "user");
    //   displayMessage(role, content);
      const messageElement = document.createElement("div");
      messageElement.classList.add(role);
      messageElement.innerText = content;
      messageElement.style.opacity = 1;
      conversation.appendChild(messageElement);
    //   const messageElement = document.createElement("div");
    //   messageElement.classList.add(i % 2 === 0 ? "assistant" : "user");
    //   messageElement.innerText = content;
    //   conversation.appendChild(messageElement);
      console.log(role, content);
      console.log(messageElement);
      console.log("hello");
    }
}
//   function sendMessage() {
//     const message = messageInput.value;
//     if (message) {
//       displayMessage("user", message);
//       messageInput.value = "";
//       setTimeout(() => {
//         displayMessage("assistant", "Sorry, I am just a demo chatbot and can't respond to messages. But I hope this chat simulation has been useful!");
//       }, 1000);
//     }
//   }

//   function displayMessage(role, content) {
//     const messageElement = document.createElement("div");
//     messageElement.classList.add(role);
//     messageElement.innerText = content;
//     conversation.appendChild(messageElement);
//   }

//   sendButton.addEventListener("click", sendMessage);
//   messageInput.addEventListener("keydown", (event) => {
//     if (event.key === "Enter") {
//       sendMessage();
//     }
//   });

//   function displayChat() {
//            let delay = 1000;
//     for (const message of chatData) {
//       const messageElement = document.createElement("div");
//       messageElement.classList.add(message.role);
//       messageElement.innerText = message.content;
//       conversation.appendChild(messageElement);

//       setTimeout(() => {
//         messageElement.style.opacity = 1;
//       }, delay);

//       delay += 1000;
//     }
//   }

// displayChat();