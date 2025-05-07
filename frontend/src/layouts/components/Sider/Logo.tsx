import { Link } from 'react-router-dom';

export default function LayoutLogo() {
  const layoutMode = useAppSelector(selectLayoutMode);
  return (
    <Link className="logo" to="/">
      <img
        style={{
          margin: layoutMode === 'sidemenu' ? '10px 16px 6px' : '2px 0 6px'
        }}
        src={`${import.meta.env.BASE_URL}logo64.png`}
      />
      {/* <h1 className="logo_text">Admin</h1> */}
    </Link>
  );
}
