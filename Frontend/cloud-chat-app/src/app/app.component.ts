import { Component, ChangeDetectorRef, OnInit } from '@angular/core';
import { LoadingService } from './services/loading.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'] // Fix: changed 'styleUrl' to 'styleUrls'
})
export class AppComponent implements OnInit {
  isLoading: boolean = false;

  constructor(private loadingService: LoadingService, private cdr: ChangeDetectorRef) { }

  ngOnInit() {
    this.loadingService.isLoading$.subscribe((loading) => {
      this.isLoading = loading;
      this.cdr.detectChanges(); // Trigger manual change detection to avoid errors
    });
  }
}