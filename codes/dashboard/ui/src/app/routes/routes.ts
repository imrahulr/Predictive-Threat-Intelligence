import { AppComponent } from '../app.component';
import { RouterModule, Routes, RouterLinkActive } from '@angular/router';

export const appRoutes: Routes = [
  { path: 'home', component: AppComponent },
  { path: '**', redirectTo: '/home', pathMatch: 'full' },
  { path: '', redirectTo: '/home', pathMatch: 'full' },
];
