import { Pipe, PipeTransform } from "@angular/core";
import { User } from "../models/user.model";

@Pipe({ name: 'userFilter' })
export class UserPipe implements PipeTransform {
    /**
     * Pipe filters the list of elements based on the search text provided
     *
     * @param userItems list of elements to search in
     * @param searchText search string
     * @returns list of elements filtered by search text or []
     */
    transform(userItems: any[], searchText: string): User[] {
        if (!userItems) {
            return [];
        }
        if (!searchText) {
            return userItems;
        }

        const result = userItems.reduce((acc, user) => {
            const c = user.username.toLocaleLowerCase();
            if (c.startsWith(searchText.toLocaleLowerCase())) {
                acc.push(user);
            }
            return acc;
        }, []);

        return result;
    }
}