import {
  Plane, Hotel, MapPin, Star, Clock, Calendar, Users, Briefcase, Luggage,
  ShieldCheck, AlertTriangle, Info, Sparkles, CheckCircle2, Circle,
  Compass, Sun, Cloud, CloudRain, CloudSnow, Snowflake, Wind,
  Ticket, Building2, Mountain, Waves, Globe, ArrowRight, Phone,
  FileText, BadgeCheck, Bed,
} from "lucide-react";

const ACCENT = "#F472B6";

const fmtINR = (n) => "₹" + Math.abs(Number(n)).toLocaleString("en-IN", { maximumFractionDigits: 0 });
const fmtINRShort = (n) => {
  const v = Math.abs(Number(n));
  if (v >= 100000) return "₹" + (v / 100000).toFixed(2) + " L";
  if (v >= 1000) return "₹" + (v / 1000).toFixed(1) + "k";
  return "₹" + v;
};

const fmtDur = (mins) => {
  const h = Math.floor(mins / 60);
  const m = mins % 60;
  return m === 0 ? `${h}h` : `${h}h ${m}m`;
};

const weatherIcon = (cond) => {
  const c = (cond || "").toLowerCase();
  if (c.includes("snow"))    return <CloudSnow size={16} style={{ color: "#bae6fd" }} />;
  if (c.includes("rain"))    return <CloudRain size={16} style={{ color: "#93c5fd" }} />;
  if (c.includes("cloud"))   return <Cloud     size={16} style={{ color: "rgba(255,255,255,0.55)" }} />;
  if (c.includes("wind"))    return <Wind      size={16} style={{ color: "rgba(255,255,255,0.55)" }} />;
  return <Sun size={16} style={{ color: "#fcd34d" }} />;
};

/* ─── TextBlock ────────────────────────────────────────── */
export function TextBlock({ content }) {
  const parts = content.split(/(\*\*[^*]+\*\*)/g);
  return (
    <div
      className="text-sm leading-relaxed px-4 py-2.5 rounded-2xl rounded-tl-md"
      style={{ background: "rgba(255,255,255,0.03)", color: "rgba(255,255,255,0.88)" }}
    >
      {parts.map((p, i) =>
        p.startsWith("**") && p.endsWith("**") ? (
          <strong key={i} className="text-white font-medium">{p.slice(2, -2)}</strong>
        ) : (
          <span key={i}>{p.split("\n").map((line, j, arr) => (
            <span key={j}>{line}{j < arr.length - 1 && <br />}</span>
          ))}</span>
        )
      )}
    </div>
  );
}

/* ─── DisclaimerBlock ──────────────────────────────────── */
export function DisclaimerBlock({ content }) {
  return (
    <div className="flex items-start gap-2.5 px-4 py-2.5 rounded-2xl border"
      style={{ background: "rgba(250, 204, 21, 0.04)", borderColor: "rgba(250, 204, 21, 0.18)", color: "rgba(250, 204, 21, 0.85)" }}>
      <Info size={14} className="mt-0.5 flex-shrink-0" />
      <div className="text-11 leading-relaxed">{content.split("\n").map((line, j, arr) => (
        <div key={j}>{line}{j < arr.length - 1 && <br />}</div>
      ))}</div>
    </div>
  );
}

/* ─── TravelAlertBlock (any safety refusal) ───────────── */
export function TravelAlertBlock({ headline, message, indicators, offer }) {
  return (
    <div className="rounded-2xl border-2 p-4 travel-pulse"
      style={{
        background: "linear-gradient(180deg, rgba(244,114,182,0.10), rgba(244,114,182,0.02))",
        borderColor: "rgba(244,114,182,0.4)",
      }}>
      <div className="flex items-center gap-2 mb-2">
        <ShieldCheck size={18} style={{ color: ACCENT }} />
        <div className="text-sm font-semibold" style={{ color: ACCENT }}>{headline}</div>
      </div>
      <div className="text-xs leading-relaxed mb-3" style={{ color: "rgba(255,255,255,0.85)" }}>{message}</div>
      <div className="space-y-1 mb-3">
        {indicators.map((it, i) => (
          <div key={i} className="flex items-start gap-2 text-11" style={{ color: "rgba(255,255,255,0.7)" }}>
            <AlertTriangle size={10} style={{ color: ACCENT, marginTop: 3, flexShrink: 0 }} />
            <span>{it}</span>
          </div>
        ))}
      </div>
      <div className="flex items-start gap-2 px-3 py-2 rounded-lg border"
        style={{ background: "rgba(255,255,255,0.04)", borderColor: ACCENT + "33" }}>
        <Sparkles size={12} style={{ color: ACCENT, marginTop: 2, flexShrink: 0 }} />
        <div className="text-11 leading-relaxed" style={{ color: "rgba(255,255,255,0.9)" }}>{offer}</div>
      </div>
    </div>
  );
}

/* ─── Flight card (used in list) ──────────────────────── */
function FlightCard({ f }) {
  return (
    <div className="rounded-xl p-3 border"
      style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
      <div className="flex items-center justify-between gap-2 mb-2">
        <div className="flex items-center gap-2 min-w-0">
          <div className="rounded-lg flex items-center justify-center flex-shrink-0"
            style={{ width: 32, height: 32, background: ACCENT + "14" }}>
            <Plane size={14} style={{ color: ACCENT }} />
          </div>
          <div className="min-w-0">
            <div className="text-xs font-medium" style={{ color: "white" }}>{f.airline}</div>
            <div className="text-9 font-mono" style={{ color: "rgba(255,255,255,0.5)" }}>{f.flight_number} · {f.aircraft}</div>
          </div>
        </div>
        <div className="text-right">
          <div className="text-sm font-mono font-medium" style={{ color: ACCENT }}>{fmtINR(f.fare_economy)}</div>
          <div className="text-9" style={{ color: "rgba(255,255,255,0.45)" }}>per pax · economy</div>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <div className="text-center" style={{ minWidth: 50 }}>
          <div className="text-sm font-mono font-medium" style={{ color: "white" }}>{f.depart}</div>
          <div className="text-9 font-mono" style={{ color: "rgba(255,255,255,0.5)" }}>{f.from.code}</div>
        </div>
        <div className="flex-1 flex flex-col items-center" style={{ paddingTop: 4 }}>
          <div className="text-9" style={{ color: "rgba(255,255,255,0.4)" }}>{fmtDur(f.duration_min)}</div>
          <div className="w-full flex items-center gap-1">
            <div style={{ width: 5, height: 5, borderRadius: "50%", background: ACCENT }} />
            <div style={{ flex: 1, height: 1, background: "rgba(255,255,255,0.15)" }} />
            <Plane size={11} style={{ color: ACCENT }} />
            <div style={{ flex: 1, height: 1, background: "rgba(255,255,255,0.15)" }} />
            <div style={{ width: 5, height: 5, borderRadius: "50%", background: ACCENT }} />
          </div>
          <div className="text-9" style={{ color: f.stops === 0 ? "#86efac" : "#fde047" }}>
            {f.stops === 0 ? "Non-stop" : `${f.stops} stop`}
          </div>
        </div>
        <div className="text-center" style={{ minWidth: 50 }}>
          <div className="text-sm font-mono font-medium" style={{ color: "white" }}>{f.arrive}</div>
          <div className="text-9 font-mono" style={{ color: "rgba(255,255,255,0.5)" }}>{f.to.code}</div>
        </div>
      </div>

      <div className="flex items-center justify-between mt-2.5 pt-2 border-t text-10"
        style={{ borderColor: "rgba(255,255,255,0.06)", color: "rgba(255,255,255,0.55)" }}>
        <div className="flex items-center gap-2">
          <span className="flex items-center gap-1"><Luggage size={9} /> {f.baggage_kg} kg</span>
          <span style={{ color: "rgba(255,255,255,0.25)" }}>·</span>
          <span style={{ color: f.refundable ? "#86efac" : "#fca5a5" }}>{f.refundable ? "Refundable" : "Non-refundable"}</span>
        </div>
        <span className="font-mono text-9" style={{ color: "rgba(255,255,255,0.35)" }}>{f.id}</span>
      </div>
    </div>
  );
}

/* ─── FlightListBlock ──────────────────────────────────── */
export function FlightListBlock({ title, route, items, total }) {
  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between px-1">
        {route && (route.from || route.to) ? (
          <div className="flex items-center gap-1.5 text-10" style={{ color: "rgba(255,255,255,0.55)" }}>
            <span className="font-mono">{route.from}</span>
            <ArrowRight size={11} style={{ color: ACCENT }} />
            <span className="font-mono">{route.to}</span>
            {route.date && (
              <>
                <span style={{ color: "rgba(255,255,255,0.3)" }}>·</span>
                <span className="flex items-center gap-1"><Calendar size={9} /> {route.date}</span>
              </>
            )}
          </div>
        ) : (
          <div className="text-10 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>{title}</div>
        )}
        <div className="text-10 font-mono" style={{ color: "rgba(255,255,255,0.55)" }}>{total} flights</div>
      </div>
      {items.map((f) => <FlightCard key={f.id} f={f} />)}
    </div>
  );
}

/* ─── FlightDetailBlock ────────────────────────────────── */
export function FlightDetailBlock({ flight: f }) {
  return (
    <div className="rounded-xl border overflow-hidden"
      style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
      <div className="px-4 py-3 border-b" style={{ borderColor: "rgba(255,255,255,0.06)", background: ACCENT + "0C" }}>
        <div className="flex items-center justify-between mb-1">
          <div className="text-sm font-medium" style={{ color: "white" }}>{f.airline} {f.flight_number}</div>
          <span className="text-9 px-1.5 py-0.5 rounded-full font-mono" style={{ background: ACCENT + "22", color: ACCENT }}>{f.id}</span>
        </div>
        <div className="text-11" style={{ color: "rgba(255,255,255,0.55)" }}>{f.aircraft} · {f.date}</div>
      </div>

      <div className="px-4 py-3 flex items-center gap-3 border-b" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
        <div className="text-center" style={{ minWidth: 70 }}>
          <div className="text-xl font-mono font-medium" style={{ color: "white" }}>{f.depart}</div>
          <div className="text-10 font-mono" style={{ color: "rgba(255,255,255,0.55)" }}>{f.from.code}</div>
          <div className="text-9" style={{ color: "rgba(255,255,255,0.45)" }}>{f.from.city}</div>
        </div>
        <div className="flex-1 flex flex-col items-center">
          <div className="text-9" style={{ color: "rgba(255,255,255,0.45)" }}>{fmtDur(f.duration_min)}</div>
          <div className="w-full flex items-center gap-1 my-1">
            <div style={{ width: 7, height: 7, borderRadius: "50%", background: ACCENT }} />
            <div style={{ flex: 1, height: 2, background: "linear-gradient(90deg, " + ACCENT + ", " + ACCENT + ")" }} />
            <Plane size={13} style={{ color: ACCENT }} />
            <div style={{ flex: 1, height: 2, background: "linear-gradient(90deg, " + ACCENT + ", " + ACCENT + ")" }} />
            <div style={{ width: 7, height: 7, borderRadius: "50%", background: ACCENT }} />
          </div>
          <div className="text-9" style={{ color: f.stops === 0 ? "#86efac" : "#fde047" }}>
            {f.stops === 0 ? "Non-stop" : `${f.stops} stop`}
          </div>
        </div>
        <div className="text-center" style={{ minWidth: 70 }}>
          <div className="text-xl font-mono font-medium" style={{ color: "white" }}>{f.arrive}</div>
          <div className="text-10 font-mono" style={{ color: "rgba(255,255,255,0.55)" }}>{f.to.code}</div>
          <div className="text-9" style={{ color: "rgba(255,255,255,0.45)" }}>{f.to.city}</div>
        </div>
      </div>

      <div className="px-4 py-3 grid grid-cols-2 gap-3 border-b" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
        <div>
          <div className="text-9 uppercase tracking-tightest2 mb-0.5" style={{ color: "rgba(255,255,255,0.4)" }}>Economy</div>
          <div className="text-sm font-mono font-medium" style={{ color: ACCENT }}>{fmtINR(f.fare_economy)}</div>
        </div>
        {f.fare_business && (
          <div>
            <div className="text-9 uppercase tracking-tightest2 mb-0.5" style={{ color: "rgba(255,255,255,0.4)" }}>Business</div>
            <div className="text-sm font-mono font-medium" style={{ color: ACCENT }}>{fmtINR(f.fare_business)}</div>
          </div>
        )}
        <div>
          <div className="text-9 uppercase tracking-tightest2 mb-0.5" style={{ color: "rgba(255,255,255,0.4)" }}>Baggage</div>
          <div className="text-xs flex items-center gap-1" style={{ color: "white" }}><Luggage size={11} /> {f.baggage_kg} kg</div>
        </div>
        <div>
          <div className="text-9 uppercase tracking-tightest2 mb-0.5" style={{ color: "rgba(255,255,255,0.4)" }}>Seats left</div>
          <div className="text-xs font-mono" style={{ color: f.seats_available < 10 ? "#fca5a5" : "white" }}>{f.seats_available}</div>
        </div>
      </div>

      <div className="px-4 py-2.5 flex items-center justify-between" style={{ background: f.refundable ? "rgba(134,239,172,0.06)" : "rgba(252,165,165,0.06)" }}>
        <div className="flex items-center gap-2">
          <ShieldCheck size={12} style={{ color: f.refundable ? "#86efac" : "#fca5a5" }} />
          <span className="text-10 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.55)" }}>
            {f.refundable ? "Refundable per fare rules" : "Non-refundable"}
          </span>
        </div>
      </div>
    </div>
  );
}

/* ─── Hotel card ───────────────────────────────────────── */
function HotelCard({ h }) {
  return (
    <div className="rounded-xl p-3 border"
      style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
      <div className="flex items-start gap-3">
        <div className="rounded-lg flex items-center justify-center flex-shrink-0"
          style={{ width: 44, height: 44, background: ACCENT + "14" }}>
          <Hotel size={18} style={{ color: ACCENT }} />
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between gap-2 mb-0.5">
            <div className="text-xs font-medium" style={{ color: "white" }}>{h.name}</div>
            <span className="text-9 px-1.5 py-0.5 rounded-full font-medium flex items-center gap-1 flex-shrink-0"
              style={{ background: h.rating >= 4.5 ? "rgba(134,239,172,0.15)" : "rgba(244,114,182,0.15)",
                       color: h.rating >= 4.5 ? "#86efac" : ACCENT }}>
              <Star size={9} fill="currentColor" /> {h.rating}
            </span>
          </div>
          <div className="flex items-center gap-1 text-10 mb-1" style={{ color: "rgba(255,255,255,0.55)" }}>
            <MapPin size={9} />
            <span>{h.area}, {h.city}</span>
            <span style={{ color: "rgba(255,255,255,0.3)" }}>·</span>
            <span>{h.category}</span>
            <span style={{ color: "rgba(255,255,255,0.3)" }}>·</span>
            <span>{"★".repeat(h.stars)}</span>
          </div>
          <div className="flex items-center justify-between">
            <div className="flex flex-wrap gap-1">
              {h.amenities.slice(0, 3).map((a, i) => (
                <span key={i} className="text-9 px-1.5 py-0.5 rounded-full"
                  style={{ background: "rgba(255,255,255,0.05)", color: "rgba(255,255,255,0.6)" }}>
                  {a}
                </span>
              ))}
              {h.amenities.length > 3 && (
                <span className="text-9 px-1.5 py-0.5" style={{ color: "rgba(255,255,255,0.45)" }}>
                  +{h.amenities.length - 3}
                </span>
              )}
            </div>
            <div className="text-right">
              <div className="text-xs font-mono font-medium" style={{ color: ACCENT }}>{fmtINR(h.price_per_night)}</div>
              <div className="text-9" style={{ color: "rgba(255,255,255,0.45)" }}>per night</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

/* ─── HotelListBlock ───────────────────────────────────── */
export function HotelListBlock({ title, items, total }) {
  return (
    <div className="space-y-2">
      {title && (
        <div className="flex items-center justify-between px-1">
          <div className="text-10 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>{title}</div>
          <div className="text-10 font-mono" style={{ color: "rgba(255,255,255,0.55)" }}>{total} hotels</div>
        </div>
      )}
      {items.map((h) => <HotelCard key={h.id} h={h} />)}
    </div>
  );
}

/* ─── HotelDetailBlock ─────────────────────────────────── */
export function HotelDetailBlock({ hotel: h }) {
  return (
    <div className="rounded-xl border overflow-hidden"
      style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
      <div className="px-4 py-3 border-b" style={{ borderColor: "rgba(255,255,255,0.06)", background: ACCENT + "0C" }}>
        <div className="flex items-center justify-between mb-1">
          <div className="text-sm font-medium" style={{ color: "white" }}>{h.name}</div>
          <span className="text-9 px-1.5 py-0.5 rounded-full font-medium flex items-center gap-1"
            style={{ background: h.rating >= 4.5 ? "rgba(134,239,172,0.15)" : "rgba(244,114,182,0.15)",
                     color: h.rating >= 4.5 ? "#86efac" : ACCENT }}>
            <Star size={9} fill="currentColor" /> {h.rating} ({h.review_count})
          </span>
        </div>
        <div className="text-11 flex items-center gap-1" style={{ color: "rgba(255,255,255,0.6)" }}>
          <MapPin size={11} /><span>{h.area}, {h.city}</span>
          <span style={{ color: "rgba(255,255,255,0.3)" }}>·</span>
          <span>{h.category}</span>
          <span style={{ color: "rgba(255,255,255,0.3)" }}>·</span>
          <span>{"★".repeat(h.stars)}</span>
        </div>
      </div>

      <div className="px-4 py-3 border-b" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
        <div className="text-10 uppercase tracking-tightest2 mb-1.5" style={{ color: "rgba(255,255,255,0.4)" }}>Room types</div>
        <div className="space-y-1.5">
          {h.room_types.map((rt, i) => (
            <div key={i} className="flex items-center justify-between gap-2 px-2 py-1.5 rounded-md"
              style={{ background: "rgba(255,255,255,0.02)" }}>
              <div className="flex items-center gap-2">
                <Bed size={11} style={{ color: ACCENT }} />
                <div>
                  <div className="text-xs" style={{ color: "white" }}>{rt.type}</div>
                  <div className="text-9" style={{ color: "rgba(255,255,255,0.5)" }}>
                    {rt.size_sqft} sqft · sleeps {rt.max_guests}
                  </div>
                </div>
              </div>
              <div className="text-right">
                <div className="text-xs font-mono" style={{ color: ACCENT }}>{fmtINR(rt.price)}</div>
                <div className="text-9" style={{ color: rt.available < 3 ? "#fca5a5" : "rgba(255,255,255,0.5)" }}>
                  {rt.available} left
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="px-4 py-3 border-b" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
        <div className="text-10 uppercase tracking-tightest2 mb-1.5" style={{ color: "rgba(255,255,255,0.4)" }}>Amenities</div>
        <div className="grid grid-cols-2 gap-1">
          {h.amenities.map((a, i) => (
            <div key={i} className="flex items-center gap-1.5 text-11" style={{ color: "rgba(255,255,255,0.75)" }}>
              <CheckCircle2 size={9} style={{ color: ACCENT }} /> {a}
            </div>
          ))}
        </div>
      </div>

      <div className="px-4 py-2.5 grid grid-cols-3 gap-3 text-10">
        <div>
          <div style={{ color: "rgba(255,255,255,0.4)" }}>Check-in</div>
          <div className="font-mono" style={{ color: "white" }}>{h.check_in}</div>
        </div>
        <div>
          <div style={{ color: "rgba(255,255,255,0.4)" }}>Check-out</div>
          <div className="font-mono" style={{ color: "white" }}>{h.check_out}</div>
        </div>
        <div>
          <div style={{ color: "rgba(255,255,255,0.4)" }}>Cancellation</div>
          <div className="text-9" style={{ color: "#86efac" }}>{h.cancellation}</div>
        </div>
      </div>
    </div>
  );
}

/* ─── PackageBlock ─────────────────────────────────────── */
export function PackageBlock({ title, items }) {
  return (
    <div className="space-y-2">
      {title && (
        <div className="text-10 uppercase tracking-tightest2 px-1" style={{ color: "rgba(255,255,255,0.4)" }}>{title}</div>
      )}
      {items.map((p) => (
        <div key={p.id} className="rounded-xl p-3 border"
          style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
          <div className="flex items-start justify-between gap-2 mb-2">
            <div className="flex items-center gap-2 min-w-0">
              <div className="rounded-lg flex items-center justify-center flex-shrink-0"
                style={{ width: 36, height: 36, background: ACCENT + "14" }}>
                <Briefcase size={15} style={{ color: ACCENT }} />
              </div>
              <div className="min-w-0">
                <div className="text-xs font-medium" style={{ color: "white" }}>{p.name}</div>
                <div className="text-10" style={{ color: "rgba(255,255,255,0.5)" }}>{p.destination} · {p.days}D / {p.nights}N</div>
              </div>
            </div>
            <div className="text-right flex-shrink-0">
              <div className="text-9 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>From</div>
              <div className="text-sm font-mono font-medium" style={{ color: ACCENT }}>{fmtINRShort(p.starts_from)}</div>
            </div>
          </div>

          <div className="text-11 italic mb-2" style={{ color: ACCENT }}>{p.highlights}</div>

          <div className="space-y-1 mb-2">
            {p.inclusions.slice(0, 4).map((inc, i) => (
              <div key={i} className="flex items-start gap-2 text-11" style={{ color: "rgba(255,255,255,0.75)" }}>
                <CheckCircle2 size={9} style={{ color: ACCENT, marginTop: 3, flexShrink: 0 }} /> {inc}
              </div>
            ))}
            {p.inclusions.length > 4 && (
              <div className="text-9 italic" style={{ color: "rgba(255,255,255,0.45)", marginLeft: 17 }}>
                + {p.inclusions.length - 4} more
              </div>
            )}
          </div>

          <div className="flex items-center justify-between pt-2 border-t text-10"
            style={{ borderColor: "rgba(255,255,255,0.06)" }}>
            <div className="flex flex-wrap gap-1">
              {p.best_for.map((b, i) => (
                <span key={i} className="text-9 px-1.5 py-0.5 rounded-full"
                  style={{ background: "rgba(255,255,255,0.05)", color: "rgba(255,255,255,0.6)" }}>
                  {b}
                </span>
              ))}
            </div>
            <span style={{ color: "rgba(255,255,255,0.5)" }}>Next: {p.next_departure}</span>
          </div>
        </div>
      ))}
    </div>
  );
}

/* ─── DestinationBlock ─────────────────────────────────── */
export function DestinationBlock({ items }) {
  return (
    <div className="space-y-2">
      {items.map((d) => (
        <div key={d.id} className="rounded-xl p-3 border"
          style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
          <div className="flex items-start gap-3 mb-2">
            <div className="rounded-lg flex items-center justify-center flex-shrink-0"
              style={{ width: 36, height: 36, background: ACCENT + "14" }}>
              <Compass size={15} style={{ color: ACCENT }} />
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between gap-2">
                <div className="text-sm font-medium" style={{ color: "white" }}>{d.name}</div>
                <span className="text-9 px-1.5 py-0.5 rounded-full font-mono"
                  style={{ background: ACCENT + "1A", color: ACCENT }}>{d.country}</span>
              </div>
              <div className="text-10 mt-0.5" style={{ color: "rgba(255,255,255,0.5)" }}>
                Best: {d.best_season} · Ideal: {d.ideal_trip_days} days
              </div>
            </div>
          </div>

          <div className="text-11 leading-relaxed mb-2" style={{ color: "rgba(255,255,255,0.75)" }}>{d.summary}</div>

          <div className="flex flex-wrap gap-1 mb-2">
            {d.highlights.map((h, i) => (
              <span key={i} className="text-9 px-1.5 py-0.5 rounded-full"
                style={{ background: ACCENT + "1A", color: ACCENT }}>{h}</span>
            ))}
          </div>

          <div className="grid grid-cols-3 gap-2 pt-2 border-t text-10"
            style={{ borderColor: "rgba(255,255,255,0.06)" }}>
            <div>
              <div style={{ color: "rgba(255,255,255,0.4)" }}>Currency</div>
              <div style={{ color: "white" }}>{d.currency}</div>
            </div>
            <div>
              <div style={{ color: "rgba(255,255,255,0.4)" }}>Language</div>
              <div className="text-9" style={{ color: "white" }}>{d.language}</div>
            </div>
            <div>
              <div style={{ color: "rgba(255,255,255,0.4)" }}>Visa</div>
              <div className="text-9" style={{ color: d.country === "India" ? "#86efac" : "#fde047" }}>
                {d.country === "India" ? "Not required (Indian)" : "Required"}
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

/* ─── ItineraryBlock ───────────────────────────────────── */
export function ItineraryBlock({ destination, nights, days, day_plan, note }) {
  return (
    <div className="rounded-xl border overflow-hidden"
      style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
      <div className="px-4 py-3 border-b flex items-center justify-between"
        style={{ borderColor: "rgba(255,255,255,0.06)", background: ACCENT + "0C" }}>
        <div className="flex items-center gap-2">
          <Calendar size={14} style={{ color: ACCENT }} />
          <span className="text-xs font-medium" style={{ color: "white" }}>{destination} itinerary</span>
        </div>
        <span className="text-10 font-mono" style={{ color: "rgba(255,255,255,0.55)" }}>{days}D / {nights}N</span>
      </div>
      <div className="px-4 py-3">
        {day_plan.map((d, i) => (
          <div key={i} className="flex gap-3 mb-3 last:mb-0">
            <div className="flex flex-col items-center flex-shrink-0">
              <div className="rounded-full flex items-center justify-center text-9 font-mono"
                style={{ width: 28, height: 28, background: ACCENT + "22", color: ACCENT, fontWeight: 600 }}>
                D{d.day}
              </div>
              {i < day_plan.length - 1 && (
                <div style={{ flex: 1, width: 2, background: "rgba(255,255,255,0.08)", marginTop: 4, minHeight: 30 }} />
              )}
            </div>
            <div className="flex-1 pb-2">
              <div className="text-xs font-medium mb-1" style={{ color: "white" }}>{d.title}</div>
              <div className="space-y-0.5">
                {d.activities.map((a, j) => (
                  <div key={j} className="flex items-start gap-1.5 text-10" style={{ color: "rgba(255,255,255,0.75)" }}>
                    <Circle size={5} style={{ color: ACCENT, marginTop: 5, flexShrink: 0, fill: "currentColor" }} />
                    <span>{a}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
      {note && (
        <div className="px-4 py-2 border-t text-10 italic"
          style={{ borderColor: "rgba(255,255,255,0.06)", color: "rgba(255,255,255,0.5)" }}>
          {note}
        </div>
      )}
    </div>
  );
}

/* ─── BookingsBlock ────────────────────────────────────── */
export function BookingsBlock({ items }) {
  return (
    <div className="space-y-2">
      <div className="text-10 uppercase tracking-tightest2 px-1" style={{ color: "rgba(255,255,255,0.4)" }}>
        Active bookings
      </div>
      {items.map((b) => (
        <div key={b.id} className="rounded-xl p-3 border"
          style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
          <div className="flex items-start gap-3">
            <div className="rounded-lg flex items-center justify-center flex-shrink-0"
              style={{ width: 36, height: 36, background: ACCENT + "14" }}>
              {b.type === "flight" ? <Plane size={15} style={{ color: ACCENT }} /> : <Hotel size={15} style={{ color: ACCENT }} />}
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between gap-2 mb-0.5">
                <div className="text-xs font-medium" style={{ color: "white" }}>{b.summary}</div>
                <span className="text-9 px-1.5 py-0.5 rounded-full font-medium flex items-center gap-1"
                  style={{ background: "rgba(134,239,172,0.15)", color: "#86efac" }}>
                  <BadgeCheck size={9} /> {b.status}
                </span>
              </div>
              <div className="text-10 mb-1.5" style={{ color: "rgba(255,255,255,0.55)" }}>{b.reference}</div>
              <div className="flex items-center justify-between text-10">
                <div className="flex items-center gap-2" style={{ color: "rgba(255,255,255,0.6)" }}>
                  <span className="flex items-center gap-1"><Calendar size={9} /> {b.date}</span>
                  <span style={{ color: "rgba(255,255,255,0.3)" }}>·</span>
                  <span className="flex items-center gap-1"><Users size={9} /> {b.pax} pax</span>
                </div>
                <span className="font-mono" style={{ color: ACCENT }}>{fmtINR(b.amount)}</span>
              </div>
              {b.checkin_open && (
                <div className="mt-1.5 pt-1.5 border-t text-10" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
                  <span style={{ color: "rgba(255,255,255,0.45)" }}>Check-in opens: </span>
                  <span style={{ color: "white" }}>{b.checkin_open}</span>
                </div>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

/* ─── BookingConfirmationBlock ─────────────────────────── */
export function BookingConfirmationBlock({ booking: b }) {
  return (
    <div className="rounded-xl border overflow-hidden"
      style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
      <div className="px-4 py-3 border-b flex items-center justify-between"
        style={{ borderColor: "rgba(255,255,255,0.06)", background: ACCENT + "0C" }}>
        <div className="flex items-center gap-2">
          {b.type === "flight" ? <Plane size={14} style={{ color: ACCENT }} /> : <Hotel size={14} style={{ color: ACCENT }} />}
          <span className="text-xs font-medium" style={{ color: "white" }}>{b.summary}</span>
        </div>
        <span className="text-9 px-1.5 py-0.5 rounded-full font-medium flex items-center gap-1"
          style={{ background: "rgba(134,239,172,0.15)", color: "#86efac" }}>
          <BadgeCheck size={9} /> {b.status}
        </span>
      </div>
      <div className="px-4 py-3 space-y-1.5 text-xs">
        <div className="flex justify-between">
          <span style={{ color: "rgba(255,255,255,0.55)" }}>Reference</span>
          <span className="font-mono" style={{ color: ACCENT }}>{b.reference}</span>
        </div>
        <div className="flex justify-between">
          <span style={{ color: "rgba(255,255,255,0.55)" }}>Booking ID</span>
          <span className="font-mono" style={{ color: "rgba(255,255,255,0.9)" }}>{b.id}</span>
        </div>
        <div className="flex justify-between">
          <span style={{ color: "rgba(255,255,255,0.55)" }}>Date</span>
          <span style={{ color: "rgba(255,255,255,0.9)" }}>{b.date}</span>
        </div>
        <div className="flex justify-between">
          <span style={{ color: "rgba(255,255,255,0.55)" }}>Travelers</span>
          <span style={{ color: "rgba(255,255,255,0.9)" }}>{b.pax} pax</span>
        </div>
        <div className="flex justify-between pt-1.5 border-t" style={{ borderColor: "rgba(255,255,255,0.08)" }}>
          <span className="font-medium" style={{ color: "white" }}>Amount</span>
          <span className="font-mono font-medium" style={{ color: ACCENT }}>{fmtINR(b.amount)}</span>
        </div>
      </div>
    </div>
  );
}

/* ─── CheckInBlock (boarding pass style) ──────────────── */
export function CheckInBlock({ booking_id, flight: f, passenger, seat, boarding_pass_ready }) {
  return (
    <div className="rounded-xl border overflow-hidden"
      style={{ background: "linear-gradient(135deg, rgba(244,114,182,0.08), rgba(255,255,255,0.02))", borderColor: ACCENT + "33" }}>
      <div className="px-4 py-3 border-b flex items-center justify-between"
        style={{ borderColor: "rgba(255,255,255,0.06)" }}>
        <div className="flex items-center gap-2">
          <Ticket size={14} style={{ color: ACCENT }} />
          <span className="text-xs font-medium tracking-tightest2 uppercase" style={{ color: "white" }}>Boarding pass</span>
        </div>
        <span className="text-9 font-mono" style={{ color: "rgba(255,255,255,0.55)" }}>{booking_id}</span>
      </div>

      <div className="px-4 py-3 border-b" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
        <div className="text-10 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>Passenger</div>
        <div className="text-sm font-medium tracking-wider" style={{ color: "white" }}>{passenger.name}</div>
        <div className="text-10" style={{ color: "rgba(255,255,255,0.55)" }}>{passenger.type} · {passenger.category}</div>
      </div>

      <div className="px-4 py-3 flex items-center gap-3 border-b" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
        <div className="text-center flex-1">
          <div className="text-9 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>From</div>
          <div className="text-xl font-mono font-medium" style={{ color: "white" }}>{f.from.code}</div>
          <div className="text-10 font-mono" style={{ color: "rgba(255,255,255,0.55)" }}>{f.depart}</div>
        </div>
        <Plane size={18} style={{ color: ACCENT, transform: "rotate(90deg)" }} />
        <div className="text-center flex-1">
          <div className="text-9 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>To</div>
          <div className="text-xl font-mono font-medium" style={{ color: "white" }}>{f.to.code}</div>
          <div className="text-10 font-mono" style={{ color: "rgba(255,255,255,0.55)" }}>{f.arrive}</div>
        </div>
      </div>

      <div className="px-4 py-3 grid grid-cols-4 gap-3 border-b" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
        <div>
          <div className="text-9 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>Flight</div>
          <div className="text-xs font-mono" style={{ color: "white" }}>{f.flight_number}</div>
        </div>
        <div>
          <div className="text-9 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>Date</div>
          <div className="text-9 font-mono" style={{ color: "white" }}>{f.date}</div>
        </div>
        <div>
          <div className="text-9 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>Gate</div>
          <div className="text-xs font-mono font-medium" style={{ color: ACCENT }}>{f.gate}</div>
        </div>
        <div>
          <div className="text-9 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.4)" }}>Seat</div>
          <div className="text-xs font-mono font-medium" style={{ color: ACCENT }}>{seat || "—"}</div>
        </div>
      </div>

      <div className="px-4 py-2.5 flex items-center justify-between"
        style={{ background: boarding_pass_ready ? "rgba(134,239,172,0.06)" : "rgba(252,165,165,0.06)" }}>
        <div className="flex items-center gap-2">
          <ShieldCheck size={12} style={{ color: boarding_pass_ready ? "#86efac" : "#fca5a5" }} />
          <span className="text-10 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.55)" }}>
            {boarding_pass_ready ? "Ready to scan" : "Awaiting check-in"}
          </span>
        </div>
        <span className="text-10 font-mono italic" style={{ color: "rgba(255,255,255,0.4)" }}>DEMO</span>
      </div>
    </div>
  );
}

/* ─── WeatherBlock ─────────────────────────────────────── */
export function WeatherBlock({ destination, forecast, note }) {
  return (
    <div className="rounded-xl border overflow-hidden"
      style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
      <div className="px-4 py-3 border-b flex items-center justify-between"
        style={{ borderColor: "rgba(255,255,255,0.06)", background: ACCENT + "0C" }}>
        <div className="flex items-center gap-2">
          <Globe size={14} style={{ color: ACCENT }} />
          <span className="text-xs font-medium" style={{ color: "white" }}>Weather · {destination}</span>
        </div>
        <span className="text-10 font-mono" style={{ color: "rgba(255,255,255,0.55)" }}>{forecast.length}-day</span>
      </div>
      <div className="px-4 py-3 grid gap-2" style={{ gridTemplateColumns: `repeat(${forecast.length}, 1fr)` }}>
        {forecast.map((d, i) => (
          <div key={i} className="text-center rounded-md py-2"
            style={{ background: "rgba(255,255,255,0.02)" }}>
            <div className="text-9 uppercase tracking-tightest2" style={{ color: "rgba(255,255,255,0.45)" }}>{d.date}</div>
            <div className="flex justify-center my-1">{weatherIcon(d.conditions)}</div>
            <div className="text-xs font-mono font-medium" style={{ color: "white" }}>{d.high}°</div>
            <div className="text-10 font-mono" style={{ color: "rgba(255,255,255,0.5)" }}>{d.low}°</div>
            <div className="text-9 mt-1" style={{ color: "rgba(255,255,255,0.55)" }}>{d.conditions}</div>
          </div>
        ))}
      </div>
      {note && (
        <div className="px-4 py-2 border-t flex items-start gap-2 text-10 italic"
          style={{ borderColor: "rgba(255,255,255,0.06)", color: "rgba(255,255,255,0.5)" }}>
          <Info size={10} style={{ marginTop: 2, flexShrink: 0 }} />
          <span>{note}</span>
        </div>
      )}
    </div>
  );
}

/* ─── VisaBlock ────────────────────────────────────────── */
export function VisaBlock({ destination, country, summary, documents, note }) {
  const groups = documents.reduce((acc, it) => {
    (acc[it.category] = acc[it.category] || []).push(it);
    return acc;
  }, {});
  return (
    <div className="rounded-xl border overflow-hidden"
      style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.08)" }}>
      <div className="px-4 py-3 border-b flex items-center justify-between"
        style={{ borderColor: "rgba(255,255,255,0.06)", background: ACCENT + "0C" }}>
        <div className="flex items-center gap-2">
          <FileText size={14} style={{ color: ACCENT }} />
          <span className="text-xs font-medium" style={{ color: "white" }}>Visa info · {destination}</span>
        </div>
        <span className="text-9 px-1.5 py-0.5 rounded-full font-mono"
          style={{ background: ACCENT + "1A", color: ACCENT }}>{country}</span>
      </div>
      <div className="px-4 py-3 border-b text-11" style={{ borderColor: "rgba(255,255,255,0.06)", color: "rgba(255,255,255,0.8)" }}>
        {summary}
      </div>
      <div className="px-4 py-3 space-y-3">
        {Object.entries(groups).map(([cat, list]) => (
          <div key={cat}>
            <div className="text-10 mb-1.5 font-medium" style={{ color: ACCENT }}>{cat}</div>
            <div className="space-y-1.5">
              {list.map((it, i) => (
                <div key={i} className="flex items-start gap-2 text-11">
                  <div className="rounded-sm flex-shrink-0 flex items-center justify-center mt-0.5"
                    style={{ width: 12, height: 12, border: `1px solid ${it.required ? ACCENT : "rgba(255,255,255,0.2)"}`, background: it.required ? ACCENT + "22" : "transparent" }}>
                    {it.required && <CheckCircle2 size={8} style={{ color: ACCENT }} />}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div style={{ color: "rgba(255,255,255,0.9)" }}>
                      {it.name}
                      {!it.required && (
                        <span className="text-9 ml-1.5 italic" style={{ color: "rgba(255,255,255,0.4)" }}>(if applicable)</span>
                      )}
                    </div>
                    <div className="text-10 mt-0.5" style={{ color: "rgba(255,255,255,0.55)" }}>{it.note}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
      {note && (
        <div className="px-4 py-2 border-t flex items-start gap-2 text-10"
          style={{ borderColor: "rgba(250, 204, 21, 0.18)", background: "rgba(250, 204, 21, 0.04)", color: "rgba(250, 204, 21, 0.85)" }}>
          <Info size={10} style={{ marginTop: 2, flexShrink: 0 }} />
          <span>{note}</span>
        </div>
      )}
    </div>
  );
}

/* ─── Dispatcher ───────────────────────────────────────── */
export default function Block({ block }) {
  switch (block.type) {
    case "text":                 return <TextBlock {...block} />;
    case "disclaimer":           return <DisclaimerBlock {...block} />;
    case "travel_alert":         return <TravelAlertBlock {...block} />;
    case "flight_list":          return <FlightListBlock {...block} />;
    case "flight_detail":        return <FlightDetailBlock {...block} />;
    case "hotel_list":           return <HotelListBlock {...block} />;
    case "hotel_detail":         return <HotelDetailBlock {...block} />;
    case "package":              return <PackageBlock {...block} />;
    case "destination":          return <DestinationBlock {...block} />;
    case "itinerary":            return <ItineraryBlock {...block} />;
    case "bookings":             return <BookingsBlock {...block} />;
    case "booking_confirmation": return <BookingConfirmationBlock {...block} />;
    case "check_in":             return <CheckInBlock {...block} />;
    case "weather":              return <WeatherBlock {...block} />;
    case "visa":                 return <VisaBlock {...block} />;
    default:
      return (
        <div className="text-xs px-3 py-2 rounded-md" style={{ background: "rgba(255,255,255,0.04)", color: "rgba(255,255,255,0.5)" }}>
          [Unknown block type: {block.type}]
        </div>
      );
  }
}
