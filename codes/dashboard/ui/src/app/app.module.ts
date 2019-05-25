import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes, RouterLinkActive } from '@angular/router';

import { AppComponent } from './app.component';

import { HttpClient, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { appRoutes } from './routes/routes';

import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { SpinnerComponent } from './features/spinner/spinner.component';
import { ToastrModule } from 'ngx-toastr';
import { ChartsModule } from 'ng2-charts';

@NgModule({
  declarations: [
    AppComponent,
    SpinnerComponent,
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot(
      appRoutes
    ),
    HttpClientModule,
    FormsModule,
    NgbModule.forRoot(),
    BrowserAnimationsModule,
    ToastrModule.forRoot({
      timeOut: 90000000,
      positionClass: 'toast-bottom-right',
      preventDuplicates: true,
      closeButton: true,

    }),
    ChartsModule, 
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }