import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { AdicionarHabitoPage } from './adicionar-habito.page';
import { RouterModule } from '@angular/router';

@NgModule({
  imports: [
    CommonModule,
    FormsModule, // Necessário para usar [(ngModel)]
    IonicModule, // Necessário para os componentes Ionic
    RouterModule.forChild([{ path: '', component: AdicionarHabitoPage }]),
  ],
  declarations: [AdicionarHabitoPage],
})
export class AdicionarHabitoPageModule {}