import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FantasyTeamComponent } from './fantasy-team.component';

describe('FantasyTeamComponent', () => {
  let component: FantasyTeamComponent;
  let fixture: ComponentFixture<FantasyTeamComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FantasyTeamComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FantasyTeamComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
