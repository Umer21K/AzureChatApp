import { inject, Injectable } from "@angular/core";
import { MatDialog } from '@angular/material/dialog';
import { DialogComponent } from "../dialog/dialog.component";
import { Subject } from "rxjs";
import { ToastrService } from "ngx-toastr";

@Injectable({
    'providedIn': 'root',
})

export class AlertService {
    error: any;

    private errorSubject = new Subject<any>();

    readonly dialog = inject(MatDialog);

    constructor(private toastr: ToastrService) { }

    toaster(type: string, title: string, message: string, time: number) {
        this.toastr.success(message, title || '', { extendedTimeOut: time, timeOut: time, positionClass: 'toast-top-right', tapToDismiss: true });
    }

    openDialog() {
        this.dialog.open(DialogComponent, { data: this.error });
    }

    emitErrorEvent(title: string, message: string) {
        this.error = { title, message };
        this.openDialog();
    }
}