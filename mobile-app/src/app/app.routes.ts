import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: 'home',
    loadComponent: () => import('./home/home.page').then((m) => m.HomePage),
  },
  {
    path: 'habito',
    loadComponent: () => import('./habito/habito.page').then((m) => m.HabitoPage), // Atualizado para refletir a nova estrutura
  },
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full',
  },
  {
    path: 'adicionar-habito',
    loadComponent: () => import('./adicionar-habito/adicionar-habito.page').then( m => m.AdicionarHabitoPage)
  },
  {
    path: 'editar-habito/:id',
    loadComponent: () => import('./editar-habito/editar-habito.page').then(m => m.EditarHabitoPage)
  },
];