import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FantasyTeamListComponent } from './fantasy-team-list.component';

describe('FantasyTeamListComponent', () => {
  let component: FantasyTeamListComponent;
  let fixture: ComponentFixture<FantasyTeamListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FantasyTeamListComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FantasyTeamListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
