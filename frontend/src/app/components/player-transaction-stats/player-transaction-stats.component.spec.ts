import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PlayerTransactionStatsComponent } from './player-transaction-stats.component';

describe('PlayerTransactionStatsComponent', () => {
  let component: PlayerTransactionStatsComponent;
  let fixture: ComponentFixture<PlayerTransactionStatsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PlayerTransactionStatsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PlayerTransactionStatsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
