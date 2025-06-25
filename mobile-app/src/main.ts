import { bootstrapApplication } from '@angular/platform-browser';
import { RouteReuseStrategy, provideRouter, withPreloading, PreloadAllModules } from '@angular/router';
import { IonicRouteStrategy, provideIonicAngular } from '@ionic/angular/standalone';
import { importProvidersFrom } from '@angular/core';

import { IonicStorageModule } from '@ionic/storage-angular';

import { addIcons } from 'ionicons';
import { addCircleOutline, createOutline, trashOutline, personCircleOutline, logOutOutline } from 'ionicons/icons';

import { routes } from './app/app.routes';
import { AppComponent } from './app/app.component';

addIcons({
  'add-circle-outline': addCircleOutline,
  'create-outline': createOutline,
  'trash-outline': trashOutline,
  'person-circle-outline': personCircleOutline,
  'log-out-outline': logOutOutline
});

bootstrapApplication(AppComponent, {
  providers: [
    importProvidersFrom(IonicStorageModule.forRoot()), // 👈 ESSA LINHA AQUI É FUNDAMENTAL
    { provide: RouteReuseStrategy, useClass: IonicRouteStrategy },
    provideIonicAngular(),
    provideRouter(routes, withPreloading(PreloadAllModules)),
  ],
});
