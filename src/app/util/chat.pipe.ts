import { Pipe, PipeTransform } from "@angular/core";
import { Room } from "../models/room.model";

@Pipe({ name: 'chatFilter' })
export class ChatPipe implements PipeTransform {
    /**
     * Pipe filters the list of elements based on the search text provided
     *
     * @param chatItems list of elements to search in
     * @param searchText search string
     * @returns list of elements filtered by search text or []
     */
    transform(chatItems: any[], searchText: string): Room[] {
        if (!chatItems) {
            return [];
        }
        if (!searchText) {
            return chatItems;
        }

        const result = chatItems.reduce((acc, chat) => {
            const c = chat.roomname.toLocaleLowerCase();
            if (c.startsWith(searchText.toLocaleLowerCase())) {
                acc.push(chat);
            }
            return acc;
        }, []);

        return result;
    }
}