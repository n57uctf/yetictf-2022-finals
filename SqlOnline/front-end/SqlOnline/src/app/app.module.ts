import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { NavigationComponent } from './navigation/navigation.component';
import { LoginComponent } from './login/login.component';
import { RegistrationComponent } from './registration/registration.component';
import { DocsComponent } from './docs/docs.component';
import { DbsComponent } from './dbs/dbs.component';
import { AboutComponent } from './about/about.component';
import { ErrorInterceptor } from '../app/_helpers/error.interceptor'; 

import { MatToolbarModule } from '@angular/material/toolbar';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field'; 
import { MatInputModule } from '@angular/material/input';
import { MatCardModule } from '@angular/material/card';
import { MatTableModule } from '@angular/material/table';
import { MatSelectModule } from '@angular/material/select'; 
import { MatDividerModule } from '@angular/material/divider'; 
import { MatGridListModule } from '@angular/material/grid-list';
import { MatListModule } from '@angular/material/list'; 
import { MatDialogModule, MAT_DIALOG_DATA } from '@angular/material/dialog'; 
 



@NgModule({
  declarations: [
    AppComponent,
    NavigationComponent,
    LoginComponent,
    RegistrationComponent,
    DocsComponent,
    DbsComponent,
    AboutComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    NoopAnimationsModule,
    MatToolbarModule,
    MatIconModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatCardModule,
    MatTableModule,
    MatSelectModule,
    MatDividerModule,
    MatGridListModule,
    MatListModule,
    MatDialogModule
  ],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true },
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
