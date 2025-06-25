import { ComponentFixture, TestBed } from '@angular/core/testing';
import { EditarHabitoPage } from './editar-habito.page';

describe('EditarHabitoPage', () => {
  let component: EditarHabitoPage;
  let fixture: ComponentFixture<EditarHabitoPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(EditarHabitoPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
