export function playKeyboardSound() {
    let audio = new Audio();
    audio.src = "/audio/keyboard-sound.wav";
    audio.load();
    audio.play();
}

export function notificationSound() {
    let audio = new Audio();
    audio.src = "/audio/notification-sound.ogg";
    audio.load();
    audio.play();
}