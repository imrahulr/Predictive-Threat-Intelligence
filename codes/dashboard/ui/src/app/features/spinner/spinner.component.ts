import { Component, OnInit , Input, OnDestroy } from '@angular/core';

@Component({
  selector: 'app-spinner',
  templateUrl: './spinner.component.html',
  styleUrls: ['./spinner.component.css']
})
export class SpinnerComponent implements OnDestroy {


  private currentTimeout: any;
  private isDelayedRunning: any = false;

  @Input()
  public delay: any = 3000;
  @Input()
  public message = 'Loading .....';

  @Input()
  public set isRunning(value: boolean) {
      if (!value) {
          this.cancelTimeout();
          this.isDelayedRunning = false;
          return;
      }

      if (this.currentTimeout) {
          return;
      }

      this.currentTimeout = setTimeout(() => {
          this.isDelayedRunning = value;
          this.cancelTimeout();
      }, this.delay);
  }

  private cancelTimeout(): void {
      clearTimeout(this.currentTimeout);
      this.currentTimeout = undefined;
  }

  ngOnDestroy(): any {
      this.cancelTimeout();
  }


}
