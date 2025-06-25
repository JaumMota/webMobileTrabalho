import { ComponentFixture, TestBed } from '@angular/core/testing';
import { AdicionarHabitoPage } from './adicionar-habito.page';

describe('AdicionarHabitoPage', () => {
  let component: AdicionarHabitoPage;
  let fixture: ComponentFixture<AdicionarHabitoPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(AdicionarHabitoPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
