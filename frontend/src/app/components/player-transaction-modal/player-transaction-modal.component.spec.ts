import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PlayerTransactionModalComponent } from './player-transaction-modal.component';

describe('PlayerTransactionModalComponent', () => {
  let component: PlayerTransactionModalComponent;
  let fixture: ComponentFixture<PlayerTransactionModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PlayerTransactionModalComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PlayerTransactionModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
