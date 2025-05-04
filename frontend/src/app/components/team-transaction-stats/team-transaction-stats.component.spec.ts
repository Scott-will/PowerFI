import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TeamTransactionStatsComponent } from './team-transaction-stats.component';

describe('TeamTransactionStatsComponent', () => {
  let component: TeamTransactionStatsComponent;
  let fixture: ComponentFixture<TeamTransactionStatsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TeamTransactionStatsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TeamTransactionStatsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
