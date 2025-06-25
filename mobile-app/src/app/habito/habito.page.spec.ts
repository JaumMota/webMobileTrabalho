import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HabitoPage } from './habito.page';

describe('HabitoPage', () => {
  let component: HabitoPage;
  let fixture: ComponentFixture<HabitoPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(HabitoPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
